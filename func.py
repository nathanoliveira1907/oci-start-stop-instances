import oci
import schedule
import time

def start_instances(compartment_id, tag_key, tag_value):
    compute_client = oci.core.ComputeClient(oci.config.from_file())
    instances = compute_client.list_instances(compartment_id).data

    for instance in instances:
        if instance.lifecycle_state == "STOPPED" and instance.freeform_tags.get(tag_key) == tag_value:
            print(f"Iniciando instância: {instance.display_name} (ID: {instance.id})")
            compute_client.instance_action(instance.id, "START")

def stop_instances(compartment_id, tag_key, tag_value):
    compute_client = oci.core.ComputeClient(oci.config.from_file())
    instances = compute_client.list_instances(compartment_id).data

    for instance in instances:
        if instance.lifecycle_state == "RUNNING" and instance.freeform_tags.get(tag_key) == tag_value:
            print(f"Desligando instância: {instance.display_name} (ID: {instance.id})")
            compute_client.instance_action(instance.id, "SOFTSTOP")

if __name__ == "__main__":
    # Defina o OCID do compartment e as tags que deseja filtrar
    compartment_id = "ocid1.compartment.oc1..aaaaaaaaf6qgwtv2obytwlf5njk4jfsxceesrrytuwsh7qxfg7blwud42tmq"  # Substitua pelo OCID do seu compartment
    tag_key = "Schedule"        # Chave da tag que está procurando
    tag_value = "StartStop"         # Valor da tag para filtrar as instâncias

    # Agendar as funções
    schedule.every().day.at("08:00").do(start_instances, compartment_id, tag_key, tag_value)
    schedule.every().day.at("20:00").do(stop_instances, compartment_id, tag_key, tag_value)

    print("Agendamentos definidos. O script está rodando...")

    while True:
        schedule.run_pending()
        time.sleep(60)  # Aguarda 1 minuto antes de verificar novamente
